// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature15Domain",
    products: [.library(name: "Feature15Domain", targets: ["Feature15Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature15Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
