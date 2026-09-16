// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature31Domain",
    products: [.library(name: "Feature31Domain", targets: ["Feature31Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature31Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
