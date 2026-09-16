// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature17Domain",
    products: [.library(name: "Feature17Domain", targets: ["Feature17Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature17Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
