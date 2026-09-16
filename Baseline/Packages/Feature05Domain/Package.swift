// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature05Domain",
    products: [.library(name: "Feature05Domain", targets: ["Feature05Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature05Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
