import Feature09Domain

public enum Feature09DataRepository {
    public static func load(_ id: Int) -> Feature09DomainModel {
        Feature09DomainModel(id: id, title: "Feature 9")
    }
}
